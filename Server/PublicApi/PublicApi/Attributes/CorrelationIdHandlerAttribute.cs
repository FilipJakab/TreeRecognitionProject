using System;
using Microsoft.AspNetCore.Mvc.Filters;

namespace PublicApi.Attributes
{
	[Obsolete]
	public class CorrelationIdHandlerAttribute : ActionFilterAttribute
	{
		public override void OnActionExecuting(ActionExecutingContext context)
		{
			if (!context.HttpContext.Items.ContainsKey("CorrelationId"))
				context.HttpContext.Items.Add("CorrelationId", Guid.NewGuid());
		}

		public override void OnActionExecuted(ActionExecutedContext context)
		{
			// context.
		}
	}
}
