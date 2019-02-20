using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace PublicApi.Interfaces
{
	public interface IHttpProvider
	{
		Task<T> Post<T>(string url, Stream fileStream, string fileName);
		
		Task<T> GetAsync<T>(string url, Dictionary<string, string> requestArgs);
	}
}
