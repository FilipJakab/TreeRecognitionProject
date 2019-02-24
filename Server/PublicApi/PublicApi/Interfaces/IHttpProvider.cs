using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace PublicApi.Interfaces
{
	public interface IHttpProvider
	{
		Task<T> PostAsync<T>(string url, object data);
		Task<T> GetAsync<T>(string url, Dictionary<string, string> requestArgs);
	}
}
