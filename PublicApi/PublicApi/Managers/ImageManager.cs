using System;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using PublicApi.Models;
using PublicApi.Providers;

namespace PublicApi.Managers
{
	public class ImageManager
	{
		private readonly ILogger<ImageManager> logger;
		private readonly HttpProvider httpProvider;

		public ImageManager(ILogger<ImageManager> logger, HttpProvider httpProvider)
		{
			this.logger = logger;
			this.httpProvider = httpProvider;
		}

		public async Task<PredictionResultsResponseModel> GetPredictionsForImage(Guid correlationId, string url, Stream fileStream, string fileName)
		{
			logger.LogDebug($"{correlationId} - Getting predictions for image of name: {fileName}");

			// TODO: Save results to DB..
			return await httpProvider.PostStream<PredictionResultsResponseModel>(correlationId, url, fileStream, fileName);
		}
	}
}