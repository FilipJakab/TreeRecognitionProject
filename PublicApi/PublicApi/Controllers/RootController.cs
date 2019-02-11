using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using NLog;
using PublicApi.Helpers;
using PublicApi.Managers;
using static PublicApi.Helpers.RequestHandler;

namespace PublicApi.Controllers
{
	[Route("api/[controller]")]
	[ApiController]
	public class RootController : ControllerBase
	{
		private readonly IConfiguration configuration;

		public RootController(IConfiguration configuration)
		{
			this.configuration = configuration;
		}

		private readonly Logger logger = LogManager.GetCurrentClassLogger();

		[HttpPost]
		[AllowAnonymous]
		public IActionResult Post([FromBody] IFormFile image)
		{
			return Handle(correlationId =>
			{

				ImageManager manager = new ImageManager();

				logger.Info($"{correlationId} - POST request for image processing");

				manager.GetPredictionsForImage(configuration.GetDeepLearningUrl(), image.OpenReadStream());
			}, Response, logger);
		}
	}
}
