using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using PublicApi.Interfaces;
using PublicApi.Models;
using PublicApi.Providers;

namespace PublicApi.Managers
{
	public class ImageManager : IImageManager
	{
		private readonly ILogger<ImageManager> logger;
		private readonly IHttpProvider httpProvider;

		public ImageManager(ILogger<ImageManager> logger, IHttpProvider httpProvider)
		{
			this.logger = logger;
			this.httpProvider = httpProvider;
		}

		public async Task<PredictionResultsResponseModel> GetPredictionsForImage(Guid correlationId, string url, string filePath)
		{
			logger.LogDebug($"{correlationId} - Getting predictions for image");

			// TODO: Save results to DB..
			return await httpProvider.Get<PredictionResultsResponseModel>(correlationId, url, new Dictionary<string, string>
			{
				{ "image", filePath }
			});
		}
	}
}
