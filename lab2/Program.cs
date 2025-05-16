using System.Reflection;
using lab2;
using Microsoft.AspNetCore.Mvc;

var assembly = Assembly.GetAssembly(typeof(ActionResult));

var allClasses = assembly.DefinedTypes.Where(s => s.IsClass);

var doi = DepthOfInheritance(allClasses);
var noc = NumberOfChildren(allClasses);
var mhf = Math.Round(MethodHidingFactor(allClasses) * 100, 2);
var ahf = Math.Round(AttributeHidingFactor(allClasses) * 100, 2);
var mif = Math.Round(MethodInheritanceFactor(allClasses) * 100, 2);
var aif = Math.Round(AttributeInheritanceFactor(allClasses) * 100, 2);
var pof = Math.Round(PolymorphismObjectFactor(allClasses) * 100, 2);


Console.WriteLine($"DOI is: {doi.Item1}. One of deepest leaf: {doi.Item2}");
Console.WriteLine($"NOC is: {noc.Item1}. Class with the most children: {noc.Item2}");
Console.WriteLine($"MHF is: {mhf}%");
Console.WriteLine($"AHF is: {ahf}%");
Console.WriteLine($"MIF is: {mif}%");
Console.WriteLine($"AIF is: {aif}%");
Console.WriteLine($"POF is: {pof}%");
return;

(int, string) DepthOfInheritance(IEnumerable<TypeInfo> types)
{
    return types.Select(type => (
        DepthOfInheritanceInternal(type),
        type.Name
    )).MaxBy(o => o.Item1);
}

int DepthOfInheritanceInternal(Type type, int currDepth = 0)
{
    return !type.BaseType.IsClass || type.BaseType == typeof(object)
        ? currDepth
        : DepthOfInheritanceInternal(type.BaseType, currDepth + 1);
}

(int, string) NumberOfChildren(IEnumerable<TypeInfo> types)
{
    return types.Select(baseClass => (
            baseClass.Assembly
                .GetTypes()
                .Count(t => t != baseClass && baseClass.IsAssignableFrom(t)),  
            baseClass.Name
        )
    ).MaxBy(o => o.Item1);
}

double MethodHidingFactor(IEnumerable<TypeInfo> types)
{
    double hiddenMethodsCount = types.Select(t => t.GetMethods(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Static)
        .Count(m => !m.IsPublic)
    ).Sum();

    double allMethodsCount = types.Select(t => t.GetMethods(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Public).Length).Sum();
    return hiddenMethodsCount / allMethodsCount;
}

double AttributeHidingFactor(IEnumerable<TypeInfo> types)
{
    double hiddenAttributesCount = types.Select(t =>
        t.GetFields(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Static)
            .Count(f => !f.IsPublic)
    ).Sum();
    
    double allAttributesCount = types.Select(t => 
        t.GetFields(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Public)
            .Length
    ).Sum();
    return hiddenAttributesCount / allAttributesCount;    
}

double MethodInheritanceFactor(IEnumerable<TypeInfo> types)
{
    double newMethods = types.Select(t =>
        t.GetMethods(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.DeclaredOnly)
            .Length
    ).Sum();
    
    double allMethods = types.Select(t =>
        t.GetMethods(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public)
            .Length
    ).Sum();

    return (allMethods - newMethods) / allMethods;
}

double AttributeInheritanceFactor(IEnumerable<TypeInfo> types)
{
    double newAttributes = types.Select(t =>
        t.GetFields(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.DeclaredOnly)
            .Length
    ).Sum();
    
    double allAttributes = types.Select(t =>
        t.GetFields(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public)
            .Length
    ).Sum();

    return (allAttributes - newAttributes) / allAttributes;
}

double PolymorphismObjectFactor(IEnumerable<TypeInfo> types)
{
    double overridenMethods = types.Select(t =>
    {
        var overridable = t.BaseType.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
            .Where(m => m.IsVirtual && !m.IsFinal)
            .ToList();

        var declared = t.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

        int overriddenCount = overridable.Count(baseMethod =>
            declared.Any(derivedMethod =>
                derivedMethod.GetBaseDefinition() == baseMethod &&
                derivedMethod.DeclaringType == t
            )
        );
        return overriddenCount;
    }).Sum();
    
    double denominator = types.Select(t =>
        t.GetMethods(
            BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly
        ).Count(m => m.IsVirtual && !m.IsFinal) *
        t.Assembly
            .GetTypes()
            .Count(assemblyTypes => assemblyTypes != t && t.IsAssignableFrom(t))
    ).Sum();
    
    return overridenMethods / denominator;
}




