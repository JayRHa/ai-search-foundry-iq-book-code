resource search 'Microsoft.Search/searchServices@2025-05-01' = {
  name: 'my-search-svc'
  location: location
  sku: { name: 'standard' }
  properties: {
    // Keyless from birth: reject API keys, accept only Entra ID.
    disableLocalAuth: true
    authOptions: null
    replicaCount: 1
    partitionCount: 1
  }
}
