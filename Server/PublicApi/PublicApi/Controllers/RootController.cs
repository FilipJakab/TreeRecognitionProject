using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PublicApi.Interfaces;
using PublicApi.Models;
using PublicApi.Models.Configurations;
using PublicApi.Services;

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
		private readonly Guid correlationId;

		public RootController(
			ILogger<RootController> logger,
			IImageManager manager,
			CorrelationService correlationService,
			IOptions<Urls> urlsOptions,
			IOptions<Paths> pathsOptions)
		{
			this.urlsOptions = urlsOptions;
			this.pathsOptions = pathsOptions;
			this.manager = manager;
			this.logger = logger;

			correlationId = correlationService.CorrelationId;
		}

		[HttpPost]
		[AllowAnonymous]
		public IActionResult Post([FromForm(Name = "image")] List<IFormFile> images)
		{
			logger.LogInformation($"{correlationId} - POST request for image processing");

			Task<PredictionResultsResponseModel> predictionsForImage = manager.ProcessImagesAsync(
				pathsOptions.Value.TemporaryFileLocation,
				urlsOptions.Value.DeepLearningApiUrl,
				images);
			predictionsForImage.Wait();

			return new ObjectResult(predictionsForImage.Result);
		}
	}
}
