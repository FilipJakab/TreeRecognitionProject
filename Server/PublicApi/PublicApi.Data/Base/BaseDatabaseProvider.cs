using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Models.Interfaces;

namespace PublicApi.Models.Base
{
	public abstract class BaseDatabaseProvider : IDatabaseProvider
	{
		private readonly Guid correlationId;
		private readonly DbContext databaseContext;
		private readonly ILogger<BaseDatabaseProvider> logger;

		protected BaseDatabaseProvider(Guid correlationId, DbContext databaseContext, ILogger<BaseDatabaseProvider> logger)
		{
			this.correlationId = correlationId;
			this.databaseContext = databaseContext;
			this.logger = logger;
		}

		public void RunInContext(Action<DbContext> magic)
		{
			try
			{
				magic(databaseContext);
			}
			catch (Exception ex)
			{
				logger.LogError(ex, $"{correlationId} - Error while executing SQL query");
			}
		}
		
		public TRes RunInContext<TRes>(Func<DbContext, TRes> magic)
		{
			try
			{
				return magic(databaseContext);
			}
			catch (Exception ex)
			{
				logger.LogError(ex, $"{correlationId} - Error while executing SQL query");
			}

			return default(TRes);
		}
	}
}
