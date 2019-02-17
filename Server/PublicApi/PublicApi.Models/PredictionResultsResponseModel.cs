using System.Collections.Generic;

namespace PublicApi.Models
{
	public class PredictionResultsResponseModel
	{
		/// <summary>
		/// Key is string representation of label and Value is confidence in percentages (0.0 to 1.0) 
		/// </summary>
		public Dictionary<string, dynamic> ImagePredictions { get; set; }

		/// <summary>
		/// Representation of timespan in seconds
		/// </summary>
		public float Taken { get; set; }

		public bool IsOk { get; set; }
	}
}
