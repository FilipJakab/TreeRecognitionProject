using System;
using System.IO;
using System.Linq;
using System.Net.Mime;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using PublicApi.Services;

namespace PublicApi.Middlewares
{
	public class UnknownErrorCatchMiddleware
	{
		private readonly RequestDelegate next;
		private readonly IHostingEnvironment env;

		public UnknownErrorCatchMiddleware(RequestDelegate next, IHostingEnvironment env)
		{
			this.next = next;
			this.env = env;
		}

		public async Task InvokeAsync(
			HttpContext context,
			ILogger<UnknownErrorCatchMiddleware> logger,
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
				context.Response.ContentType = "application/json";
				if (env.IsDevelopment())
					context.Response.Body.Write(JsonConvert.SerializeObject(ex, new JsonSerializerSettings
					{
						ReferenceLoopHandling = ReferenceLoopHandling.Ignore
					}).Select(x => (byte) x).ToArray());
				else
					throw;
			}
		}
	}
}
