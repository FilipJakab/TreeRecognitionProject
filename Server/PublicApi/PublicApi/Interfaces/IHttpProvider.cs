using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace PublicApi.Interfaces
{
	public interface IHttpProvider
	{
		Task<T> Post<T>(Guid correlationId, string url, Stream fileStream, string fileName);
		
		Task<T> Get<T>(Guid correlationId, string url, Dictionary<string, string> requestArgs);
	}
}
