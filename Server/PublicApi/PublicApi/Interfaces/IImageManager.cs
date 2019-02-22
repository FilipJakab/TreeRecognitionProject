using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using PublicApi.Data;

namespace PublicApi.Interfaces
{
	public interface IImageManager
	{
		Task<ResponseModel> ProcessImagesAsync(string tempFolderPath, string url, List<IFormFile> files);
	}
}
