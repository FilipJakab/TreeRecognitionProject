using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PublicApi.Helpers;
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
		private readonly ImageManager manager;
		private readonly ILogger<RootController> logger;

		public RootController(ILogger<RootController> logger, IOptions<Urls> urlsOptions, ImageManager manager)
		{
			this.urlsOptions = urlsOptions;
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

				Task<PredictionResultsResponseModel> predictionsForImage = manager.GetPredictionsForImage(
					correlationId,
					urlsOptions.Value.DeepLearningApiUrl,
					image.OpenReadStream(),
					image.FileName);
				predictionsForImage.Wait();

				return predictionsForImage.Result;
			}, Response, logger);
		}
	}
}