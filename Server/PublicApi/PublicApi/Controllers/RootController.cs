using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PublicApi.Helpers;
using PublicApi.Interfaces;
using PublicApi.Managers;
using PublicApi.Models;
using PublicApi.Models.Configurations;
using static PublicApi.Helpers.RequestHandler;

namespace PublicApi.Controllers
{
	[Route("api")]
	[ApiController]
	public class RootController : ControllerBase
	{
		private readonly IOptions<Urls> urlsOptions;
		private readonly IOptions<Paths> pathsOptions;
		private readonly IImageManager manager;
		private readonly ILogger<RootController> logger;

		public RootController(
			ILogger<RootController> logger,
			IImageManager manager,
			IOptions<Urls> urlsOptions,
			IOptions<Paths> pathsOptions)
		{
			this.urlsOptions = urlsOptions;
			this.pathsOptions = pathsOptions;
			this.manager = manager;
			this.logger = logger;
		}

		[HttpPost]
		[AllowAnonymous]
		public IActionResult Post([FromForm(Name = "image")] IFormFile image)
		{
			return Handle((correlationId, logger) =>
			{
				logger.LogInformation($"{correlationId} - POST request for image processing");

				string newFilename =
					FileHelper.GetNewFileName(pathsOptions.Value.TemporaryFileLocation, Path.GetExtension(image.FileName));
				FileInfo newFile = new FileInfo(newFilename);
				using (Stream target = newFile.Create())
					image.CopyTo(target);

				Task<PredictionResultsResponseModel> predictionsForImage = manager.GetPredictionsForImage(
					correlationId,
					urlsOptions.Value.DeepLearningApiUrl,
					newFile.FullName);
				predictionsForImage.Wait();

				return predictionsForImage.Result;
			}, Response, logger);
		}
	}
}
