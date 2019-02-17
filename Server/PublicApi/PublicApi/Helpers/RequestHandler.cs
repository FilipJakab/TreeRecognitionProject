using System;
using System.Data.SqlClient;
using System.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.Extensions.Logging;
using PublicApi.Models;
using PublicApi.Resources;

namespace PublicApi.Helpers
{
	public static class RequestHandler
	{
		public static IActionResult Handle<T>(Func<Guid, ILogger, T> what, HttpResponse response, ILogger logger)
		{
			Guid correlationId = Guid.NewGuid();

			ResponseModel<T> result = new ResponseModel<T>
			{
				Data = default(T),
				Metrics = new Metrics
				{
					Started = DateTime.Now
				},
				IsOk = false
			};

			Stopwatch watch = Stopwatch.StartNew();

			try
			{
				result.Data = what(correlationId, logger);

				result.IsOk = true;
			}
			catch (SqlException ex)
			{
				logger.LogError(ex, $"{correlationId} - Error while communicating with Database");
				result.ErrorMessage = ex.Message;
			}
			catch (Exception ex)
			{
				logger.LogError(ex, $"{correlationId} - Error occured while processing request.");
				// result.ErrorMessage = ex.Message;
				result.Exception = ex;
			}

			if (!result.IsOk)
				result.ErrorMessage = CommonMessages.UnknownError;
			result.Metrics.TimeTaken = watch.Elapsed;

			response.StatusCode = result.IsOk
				? StatusCodes.Status200OK
				: StatusCodes.Status500InternalServerError;

			return new ObjectResult(result);
		}
	}
}