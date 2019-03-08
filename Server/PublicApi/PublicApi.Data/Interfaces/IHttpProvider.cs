using System.Collections.Generic;
using System.Threading.Tasks;

namespace PublicApi.Data.Interfaces
{
	public interface IHttpProvider
	{
		Task<T> PostAsync<T>(string url, object data);
		Task<T> GetAsync<T>(string url, Dictionary<string, string> requestArgs);
	}
}
