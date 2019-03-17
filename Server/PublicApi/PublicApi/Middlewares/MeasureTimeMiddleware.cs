using System.Data.SqlClient;
using System.Diagnostics;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Primitives;
using PublicApi.Services;

namespace PublicApi.Middlewares
{
	public class MeasureTimeMiddleware
	{
		private readonly RequestDelegate next;

		public MeasureTimeMiddleware(RequestDelegate next)
		{
			this.next = next;
		}

		public async Task InvokeAsync(HttpContext context)
		{
			Stopwatch watch = Stopwatch.StartNew();
			
			context.Response.OnStarting(state =>
			{
				((HttpContext) state).Response
					.Headers.Add(
						"X-ElapsedTicks",
						new StringValues(watch.ElapsedTicks.ToString())
					);

				return Task.CompletedTask;
			}, context);
			
			await next.Invoke(context);

			// context.Response.Headers.Add("ElapsedTicks", new StringValues(watch.ElapsedTicks.ToString()));
		}
	}
}
