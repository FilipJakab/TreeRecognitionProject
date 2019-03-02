using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace PublicApi.Data.Interfaces
{
	public interface IImageManager
	{
		Task<ResponseModel> ProcessImagesAsync(string tempFolderPath, string url, List<IFormFile> files);
	}
}
