using System;
using System.Collections.Generic;
using PublicApi.Database;

namespace PublicApi.Data.Interfaces
{
	public interface ITreeRecognitionDbProvider
	{
		WebRequest RegisterRequest(Guid webRequestCorrelationId);

		void RegisterImageDefinition(ImageDefinition imageDefinition);

		PredictionRequest RegisterPredictionRequest(int webRequestId, int imageId);

		void RegisterPredictionResults(List<PredictionResult> results);

		void RegisterMetrics(Metric metrics);
	}
}
