using System.Collections.Generic;

namespace PublicApi.Data
{
	public class PredictionRequestModel
	{
		/// <summary>
		/// List of image paths
		/// </summary>
		public List<string> Images { get; set; }

		public PredictionRequestModel(List<string> imagePaths)
		{
			Images = imagePaths;
		}
	}
}
