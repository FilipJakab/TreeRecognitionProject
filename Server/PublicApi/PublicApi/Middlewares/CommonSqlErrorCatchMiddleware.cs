using System;
using System.Data.SqlClient;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using PublicApi.Services;

namespace PublicApi.Middlewares
{
	public class CommonSqlErrorCatchMiddleware
	{
		private readonly RequestDelegate next;

		public CommonSqlErrorCatchMiddleware(RequestDelegate next)
		{
			this.next = next;
		}

		public async Task InvokeAsync(HttpContext context, ILogger<CommonSqlErrorCatchMiddleware> logger, CorrelationService correlationService)
		{
			try
			{
				await next.Invoke(context);
			}
			catch (SqlException ex)
			{
				logger.LogError(ex, $"{correlationService.CorrelationId} - Error while communicating with Database");

				context.Response.StatusCode = StatusCodes.Status500InternalServerError;
			}
		}
	}
}
