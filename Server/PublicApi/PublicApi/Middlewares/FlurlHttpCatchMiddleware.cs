using System.Data.SqlClient;
using System.Threading.Tasks;
using Flurl.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using PublicApi.Services;

namespace PublicApi.Middlewares
{
	public class FlurlHttpCatchMiddleware
	{
		private readonly RequestDelegate next;

		public FlurlHttpCatchMiddleware(RequestDelegate next)
		{
			this.next = next;
		}

		public async Task InvokeAsync(HttpContext context, ILogger<CommonSqlErrorCatchMiddleware> logger, CorrelationService correlationService)
		{
			try
			{
				await next.Invoke(context);
			}
			catch (FlurlHttpException ex)
			{
				logger.LogError(ex, $"{correlationService.CorrelationId} - Error while communicating with DeepLearning API");

				context.Response.StatusCode = StatusCodes.Status500InternalServerError;
			}
		}
	}
}
