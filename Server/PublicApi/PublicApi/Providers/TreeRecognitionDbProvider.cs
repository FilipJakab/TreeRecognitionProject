using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Database;
using PublicApi.Models.Base;

namespace PublicApi.Providers
{
	public class TreeRecognitionDbProvider : BaseDatabaseProvider
	{
		public TreeRecognitionDbProvider(
			Guid correlationId,
			TreeRecognitionDbContext databaseContext,
			ILogger<BaseDatabaseProvider> logger) : base(correlationId, databaseContext, logger)
		{  }

		public void RegisterRequest(string fileName)
		{
			
		}
	}
}
