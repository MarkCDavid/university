Install-PackageProvider -Name "NuGet" | Out-Null
Install-Package -Name System.Security.Cryptography.ProtectedData -ProviderName NuGet -Scope CurrentUser -RequiredVersion 7.0.0 -SkipDependencies -Destination . -Force -Source NuGet | Out-Null
Move-Item ".\System.Security.Cryptography.ProtectedData.7.0.0\lib\net462\System.Security.Cryptography.ProtectedData.dll" "C:\Users\vagrant\System.Security.Cryptography.ProtectedData.dll" | Out-Null

$assemblies=(
    "System",
    "System.Runtime",
    "System.Security",
    "System.Security.Cryptography.ProtectedData"
)

$source=@"
using System;
using System.Text;
using System.Security.Cryptography;

namespace pGina {
    public static class Helper {
        public static string Encrypt(string value){
            return Convert.ToBase64String(ProtectedData.Protect(Encoding.UTF8.GetBytes(value), null, DataProtectionScope.LocalMachine));
        }
    }
}
"@

Add-Type -ReferencedAssemblies $assemblies -TypeDefinition $source -Language CSharp | Out-Null
[pGina.Helper]::Encrypt("password")
