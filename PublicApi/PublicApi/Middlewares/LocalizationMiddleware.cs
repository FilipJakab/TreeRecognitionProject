using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace PublicApi.Middlewares
{
	public class LocalizationMiddleware
	{
		private readonly RequestDelegate next;

		public LocalizationMiddleware(RequestDelegate next)
		{
			this.next = next;
		}

		public async Task InvokeAsync(HttpContext ctx)
		{
			await next.Invoke(ctx);
		}
	}
}