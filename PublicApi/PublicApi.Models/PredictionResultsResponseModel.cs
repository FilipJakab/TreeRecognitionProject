using System.Collections.Generic;

namespace PublicApi.Models
{
	public class PredictionResultsResponseModel
	{
		public IDictionary<string, int> Predictions { get; set; }

		public Metrics Metrics { get; set; }

		public bool IsOk { get; set; }
	}
}