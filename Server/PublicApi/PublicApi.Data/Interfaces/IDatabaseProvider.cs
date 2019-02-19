using System;
using Microsoft.EntityFrameworkCore;

namespace PublicApi.Models.Interfaces
{
	public interface IDatabaseProvider
	{
		void RunInContext(Action<DbContext> magic);

		T RunInContext<T>(Func<DbContext, T> magic);
	}
}