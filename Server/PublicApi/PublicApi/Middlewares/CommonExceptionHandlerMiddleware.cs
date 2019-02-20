using System;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using PublicApi.Services;

namespace PublicApi.Middlewares
{
	public class CommonExceptionHandlerMiddleware
	{
		private readonly RequestDelegate next;

		public CommonExceptionHandlerMiddleware(RequestDelegate next)
		{
			this.next = next;
		}

		public async Task InvokeAsync(HttpContext context, ILogger<CommonExceptionHandlerMiddleware> logger,
			CorrelationService correlationService)
		{
			try
			{
				await next.Invoke(context);
			}
			catch (Exception ex)
			{
				logger.LogError(ex,
					$"{correlationService.CorrelationId} - Unknown error occured while processing your request");

				context.Response.StatusCode = StatusCodes.Status500InternalServerError;
				context.Response.Body.Write(JsonConvert.SerializeObject(ex).Select(x => (byte)x).ToArray());
			}
		}
	}
}
