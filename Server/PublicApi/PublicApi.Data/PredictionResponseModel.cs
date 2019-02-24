using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace PublicApi.Data
{
	public class PredictionResponseModel
	{
		public List<Dictionary<string, float>> Data { get; set; }
		public bool IsOk { get; set; }
		public TimeSpan Taken { get; set; }
	}
}
