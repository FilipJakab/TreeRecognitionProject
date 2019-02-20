using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using PublicApi.Models;

namespace PublicApi.Interfaces
{
	public interface IImageManager
	{
		Task<PredictionResultsResponseModel> ProcessImagesAsync(string tempFolderPath, string url, List<IFormFile> files);
	}
}
