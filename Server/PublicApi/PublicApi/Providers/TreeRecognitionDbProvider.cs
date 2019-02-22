using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Database;
using PublicApi.Data;
using PublicApi.Data.Base;
using PublicApi.Data.Interfaces;
using PublicApi.Services;

namespace PublicApi.Providers
{
	public class TreeRecognitionDbProvider : BaseDatabaseProvider<TreeRecognitionDbContext>, ITreeRecognitionDbProvider
	{
		private readonly ILogger<BaseDatabaseProvider<TreeRecognitionDbContext>> logger;
		private readonly Guid correlationId;
		
		public TreeRecognitionDbProvider(
			TreeRecognitionDbContext databaseContext,
			CorrelationService correlationService,
			ILogger<BaseDatabaseProvider<TreeRecognitionDbContext>> logger) : base(databaseContext, logger,
			correlationService.CorrelationId)
		{
			this.logger = logger;
			correlationId = correlationService.CorrelationId;
		}

		public WebRequest RegisterRequest(Guid webRequestCorrelationId)
		{
			logger.LogTrace($"{correlationId} - Registering WebRequest for CorrelationId {webRequestCorrelationId}");
			
			WebRequest webRequest = new WebRequest
			{
				CorrelationId = webRequestCorrelationId
			};
			
			RunWithContext(ctx =>
			{
				ctx.WebRequest.Add(webRequest);
				ctx.SaveChanges();
			});

			return webRequest;
		}

		public void RegisterImageDefinition(ImageDefinition imageDefinition)
		{
			logger.LogTrace($"{correlationId} - Registering ImageDefinition for image \"{imageDefinition.OriginalFileName}\"");
			
			RunWithContext(ctx =>
			{
				ctx.ImageDefinition.Add(imageDefinition);
				ctx.SaveChanges();
			});
		}

		public PredictionRequest RegisterPredictionRequest(int webRequestId, int imageId)
		{
			logger.LogTrace($"{correlationId} - Registering PredictionRequest for image id {imageId}");
			
			PredictionRequest predictionRequest = new PredictionRequest
			{
				WebRequestId = webRequestId,
				ImageId = imageId
			};
			
			RunWithContext(ctx =>
			{
				ctx.PredictionRequest.Add(predictionRequest);
				ctx.SaveChanges();
			});

			return predictionRequest;
		}

		public void RegisterPredictionResults(List<PredictionResult> results)
		{
			logger.LogTrace($"{correlationId} - Registering {results.Count} PredictionResults");
			RunWithContext(ctx =>
			{
				ctx.PredictionResult.AddRange(results);
				ctx.SaveChanges();
			});
		}

		public void RegisterMetrics(Metric metrics)
		{
			logger.LogTrace($"{correlationId} - Registering metrics for WebRequests Id {metrics.WebRequestId}");
			RunWithContext(ctx =>
			{
				ctx.Metric.Add(metrics);
				ctx.SaveChanges();
			});
		}
	}
}
