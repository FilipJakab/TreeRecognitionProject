using System;
using System.Data.SqlClient;
using System.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using NLog;
using PublicApi.Models;
using PublicApi.Resources;

namespace PublicApi.Helpers
{
	public static class RequestHandler
	{
		public static IActionResult Handle<T>(Func<Guid, Logger, T> what, HttpResponse response, Logger logger)
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
				logger.Error(ex, $"{correlationId} - Error while communicating with Database");

				result.ErrorMessage = ResponseErrorMessages.SqlError;
			}
			catch (Exception ex)
			{
				logger.Error(ex, $"{correlationId} - Error occured while processing request.");

				result.ErrorMessage = ResponseErrorMessages.UnknownError;
			}

			result.Metrics.TimeTaken = watch.Elapsed;

			response.StatusCode = result.IsOk
				? StatusCodes.Status200OK
				: StatusCodes.Status500InternalServerError;

			return new ObjectResult(result);
		}
	}
}