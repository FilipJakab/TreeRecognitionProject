using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using PublicApi.Models;

namespace PublicApi.Interfaces
{
	public interface IImageManager
	{
		Task<PredictionResultsResponseModel> GetPredictionsForImage(Guid correlationId, string url, string filePath);
	}
}
