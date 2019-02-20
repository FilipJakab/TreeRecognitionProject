using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using ExifLib;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using PublicApi.Database;
using PublicApi.Helpers;
using PublicApi.Interfaces;
using PublicApi.Models;
using PublicApi.Models.Interfaces;
using PublicApi.Services;

namespace PublicApi.Managers
{
	public class ImageManager : IImageManager
	{
		private readonly ILogger<ImageManager> logger;
		private readonly ITreeRecognitionDbProvider dbProvider;
		private readonly IHttpProvider httpProvider;
		private readonly Guid correlationId;

		public ImageManager(
			ITreeRecognitionDbProvider dbProvider,
			IHttpProvider httpProvider,
			ILogger<ImageManager> logger,
			CorrelationService correlationService)
		{
			this.logger = logger;
			this.dbProvider = dbProvider;
			this.httpProvider = httpProvider;

			correlationId = correlationService.CorrelationId;
		}

		/// <summary>
		/// Handles one round of Handling images (i.e. image saving, registering in Database, getting results for each image
		/// </summary>
		/// <param name="tempFolderPath">Path where to store file</param>
		/// <param name="url">Url at which DeepLearningAPI is server</param>
		/// <param name="files">Files (images) to be processed</param>
		/// <returns></returns>
		public async Task<PredictionResultsResponseModel> ProcessImagesAsync(
			string tempFolderPath,
			string url,
			List<IFormFile> files)
		{
			logger.LogDebug($"{correlationId} - Getting predictions for {files.Count} images");

			Dictionary<string, string> getQuery = new Dictionary<string, string>(files.Count);
			List<PredictionRequest> predictionRequests = new List<PredictionRequest>(files.Count);

			DateTime started = DateTime.Now;
			WebRequest webRequest = dbProvider.RegisterRequest(correlationId);
			// Asynchronously save files and extract their EXIF data
			files.ForEach(file =>
			{
				using (Stream fileStream = file.OpenReadStream())
				{
					string generatedFileName = SaveFile(tempFolderPath, fileStream, file.FileName);

					ImageDefinition imageDefinition = new ImageDefinition();

					logger.LogDebug($"{correlationId} - Extracting EXIF data from {file.FileName}");
					ExtractExifData(imageDefinition, fileStream);

					imageDefinition.OriginalFileName = file.FileName;
					imageDefinition.Size = file.Length;
					imageDefinition.WebRequestId = webRequest.WebRequestId;
					logger.LogDebug($"{correlationId} - Registering ImageDefinition of {file.FileName} file to Database");
					dbProvider.RegisterImageDefinition(imageDefinition);
					predictionRequests.Add(
						dbProvider.RegisterPredictionRequest(webRequest.WebRequestId, imageDefinition.ImageDefinitionId));
					getQuery.Add("image", generatedFileName);
				}
			});

			// Send actual request
			logger.LogDebug($"{correlationId} - Sending request for predictions to \"{url}\"");
			PredictionResultsResponseModel response = await httpProvider
				.GetAsync<PredictionResultsResponseModel>(url, getQuery);

			// TODO: Save results to DB..
			// List<PredictionResult> results = new List<PredictionResult>();
			List<PredictionResult> allPredictionResults = response.ImagePredictions.Select((imagePredictions, i) =>
					imagePredictions.Select(prediction => new PredictionResult
					{
						Label = prediction.Key,
						Score = prediction.Value,
						PredictionRequestId = predictionRequests[i].PredictionRequestId
					}).ToList())
				.Aggregate((predictions1, predictions2) =>
				{
					predictions1.AddRange(predictions2);
					return predictions1;
				});

			dbProvider.RegisterPredictionResults(allPredictionResults);

			// TODO: Register Metrics
			dbProvider.RegisterMetrics(new Metric
			{
				WebRequestId = webRequest.WebRequestId,
				Started = started,
				Ended = DateTime.Now
			});

			return response;
		}

		/// <summary>
		/// Gets Exif data from <see cref="ExifReader"/> and fill those data into <see cref="ImageDefinition"/>
		/// </summary>
		/// <param name="imageDefinition"></param>
		/// <param name="fileStream"></param>
		private void ExtractExifData(ImageDefinition imageDefinition, Stream fileStream)
		{
			fileStream.Seek(0, SeekOrigin.Begin);
			using (ExifReader exifReader = new ExifReader(fileStream))
			{
				if (exifReader.GetTagValue(ExifTags.Make, out string vendor))
					imageDefinition.CameraVendor = vendor;
				if (exifReader.GetTagValue(ExifTags.Model, out string model))
					imageDefinition.CameraModel = model;
				if (exifReader.GetTagValue(ExifTags.DateTimeOriginal, out DateTime date))
					imageDefinition.Taken = date;
				if (exifReader.GetTagValue(ExifTags.Compression, out string compression))
					imageDefinition.Compression = compression;
				if (exifReader.GetTagValue(ExifTags.XResolution, out double xResolution)) // double
					imageDefinition.Xresolution = xResolution;
				if (exifReader.GetTagValue(ExifTags.YResolution, out double yResolution))
					imageDefinition.Yresolution = yResolution;
				if (exifReader.GetTagValue(ExifTags.ResolutionUnit, out ushort resolutionUnit)) // uint16
					imageDefinition.ResolutionUnit = (short)resolutionUnit;
				if (exifReader.GetTagValue(ExifTags.ExposureTime, out double exposureTime)) // double
					imageDefinition.ExposureTime = exposureTime;
				if (exifReader.GetTagValue(ExifTags.ExposureProgram, out ushort exposureProgram)) // uint16
					imageDefinition.ExposureProgram = (short)exposureProgram;
				if (exifReader.GetTagValue(ExifTags.ExifVersion, out byte[] exifVersion)) // byte[]
					imageDefinition.ExifVersion = exifVersion;
				if (exifReader.GetTagValue(ExifTags.ComponentsConfiguration, out byte[] componentsConfiguration)) // byte[]
					imageDefinition.ComponentConfiguration = componentsConfiguration;
				if (exifReader.GetTagValue(ExifTags.ExposureBiasValue, out double exposureBias))
					imageDefinition.ExposureBias = exposureBias;
				if (exifReader.GetTagValue(ExifTags.MaxApertureValue, out double maxAperture))
					imageDefinition.MaxApertureValue = maxAperture;
				if (exifReader.GetTagValue(ExifTags.ApertureValue, out double aperture))
					imageDefinition.ApertureValue = aperture;
				if (exifReader.GetTagValue(ExifTags.Flash, out ushort flash)) // uint16
					imageDefinition.Flash = (short)flash;
				if (exifReader.GetTagValue(ExifTags.ColorSpace, out ushort colorSpace)) // uint16
					imageDefinition.ColorSpace = (short)colorSpace;
				if (exifReader.GetTagValue(ExifTags.ImageWidth, out int width))
					imageDefinition.Width = width;
				if (exifReader.GetTagValue(ExifTags.ImageWidth, out int height))
					imageDefinition.Width = height;
				if (exifReader.GetTagValue(ExifTags.Orientation, out string orientation))
					imageDefinition.Orientation = orientation;
			}
		}

		/// <summary>
		/// Saves file on disk asynchronously and returns file's filename
		/// </summary>
		/// <param name="tempFolderPath"></param>
		/// <param name="file"></param>
		/// <param name="fileName"></param>
		/// <returns></returns>
		private string SaveFile(string tempFolderPath, Stream file, string fileName)
		{
			logger.LogDebug($"{correlationId} - file \"{fileName}\" is being saved to \"{tempFolderPath}\"");

			string newFilename = FileHelper
				.GetNewFileName(tempFolderPath, Path.GetExtension(fileName));
			FileInfo newFile = new FileInfo(newFilename);

			using (Stream target = newFile.Create())
				file.CopyTo(target);
			return newFilename;
		}
	}
}
