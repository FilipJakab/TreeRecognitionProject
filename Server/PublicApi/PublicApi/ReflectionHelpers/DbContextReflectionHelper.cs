using System;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;

namespace PublicApi.ReflectionHelpers
{
	public class DbContextReflectionHelper
	{
		private MethodInfo[] _getEnumerableMethods;
		private MethodInfo[] _getQueryableMethods;

		private MethodInfo _toList;
		private MethodInfo _where;
		private MethodInfo _take;
		private MethodInfo _remove;

		/// <summary>
		/// 
		/// </summary>
		/// <param name="dbSet"></param>
		/// <param name="object"></param>
		/// <returns>EntityEntry</returns>
		public object Remove(object dbSet, object @object)
		{
			MethodInfo genericRemove = getRemove()
				.MakeGenericMethod(dbSet.GetType().GenericTypeArguments);

			return genericRemove.Invoke(null, new [] {dbSet, @object});
		}
		
		public object Take(object dbSet, int amount)
		{
			MethodInfo genericTake = getTake()
				.MakeGenericMethod(dbSet.GetType().GenericTypeArguments);

			return genericTake.Invoke(null, new [] {dbSet, amount});
		}

		/// <summary>
		/// 
		/// </summary>
		/// <param name="dbSet"></param>
		/// <param name="predicate"></param>
		/// <typeparam name="T"></typeparam>
		/// <returns>IQueryable</returns>
		public object Where(object dbSet, Expression<Func<object, bool>> predicate)
		{
			MethodInfo genericWhere = getWhere()
				.MakeGenericMethod(dbSet.GetType().GenericTypeArguments);

			// modify predicate to have param of type dbSet<X>
			// Type predicateType = predicate.GetType();
			// Type predicateFuncType = predicateType.GenericTypeArguments.Single();
			// Type predicateFuncTypeGeneralized = predicateFuncType.MakeGenericType(dbSet.PropertyType.GenericTypeArguments.Single(), typeof(bool));
			// // Cast predicate to new Type
			// MethodInfo toFuncTypeGeneralizedCaster = GetType().GetMethod(nameof(Cast)).MakeGenericMethod(predicateFuncTypeGeneralized);
			// object castedPredicate = toFuncTypeGeneralizedCaster.Invoke(this, new object[] {predicate});
			// object castedExpression = 

			// predicate
			return genericWhere.Invoke(null, new [] {dbSet, predicate});
		}

		/// <summary>
		/// 
		/// </summary>
		/// <param name="dbSet"></param>
		/// <returns>List</returns>
		public object ToList(object dbSet)
		{
			// Retrieve .ToList Method

			MethodInfo genericToList = getToList()
				.MakeGenericMethod(dbSet.GetType().GenericTypeArguments);

			return genericToList.Invoke(null, new[] {dbSet});
		}

		private TOut Cast<TOut>(object o)
		{
			return (TOut) o;
		}

		#region GetCaches

		private MethodInfo getRemove()
		{
			if (_remove != null)
				return _remove;

			return _remove = getQueryableMethods()
				.First(method => method.Name == "Remove");
		}
		
		private MethodInfo getTake()
		{
			if (_take != null)
				return _take;

			return _take = getQueryableMethods()
				.First(method => method.Name == "Take");
		}
		
		private MethodInfo getWhere()
		{
			if (_where != null)
				return _where;

			return _where = getQueryableMethods()
				.First(method => method.Name == "Where");
		}

		private MethodInfo getToList()
		{
			if (_toList != null)
				return _toList;

			return _toList = getEnumerableMethods()
				.First(method => method.Name == "ToList");
		}

		private MethodInfo[] getEnumerableMethods()
		{
			if (_getEnumerableMethods != null)
				return _getEnumerableMethods;

			return _getEnumerableMethods = typeof(Enumerable)
				.GetMethods(BindingFlags.Public | BindingFlags.Static);
		}
		
		private MethodInfo[] getQueryableMethods()
		{
			if (_getQueryableMethods != null)
				return _getQueryableMethods;

			return _getQueryableMethods = typeof(Queryable)
				.GetMethods(BindingFlags.Public | BindingFlags.Static);
		}

		#endregion
	}
}
