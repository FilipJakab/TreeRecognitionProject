using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Data.Interfaces;

namespace PublicApi.Data.Base
{
	public abstract class BaseDatabaseProvider<TDbContext>
	{
		private readonly TDbContext databaseContext;
		private readonly ILogger<BaseDatabaseProvider<TDbContext>> logger;
		private readonly Guid correlationId;

		protected BaseDatabaseProvider(TDbContext databaseContext,
			ILogger<BaseDatabaseProvider<TDbContext>> logger,
			Guid correlationId)
		{
			this.databaseContext = databaseContext;
			this.correlationId = correlationId;
			this.logger = logger;
		}

		protected void RunWithContext(Action<TDbContext> magic)
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

		protected TRes RunWithContext<TRes>(Func<TDbContext, TRes> magic)
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
