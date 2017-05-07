function getResourceComponent(organizedResources){
  var components = [];
  var resourceTypes = ['basic', 'earned'];
  var resources = [];
  var resourceType;
  var resource;
  var count;
  for (var i=0; i<resourceTypes.length; i++){
    resourceType = resourceTypes[i];
    if (organizedResources.hasOwnProperty(resourceType)){
      resources = organizedResources[resourceType];
      components.push(<h5>{resourceType}</h5>);
      for (resource in resources){
        if (resources.hasOwnProperty(resource)){
          count = resources[resource];
          components.push(
            <div>
              <SpanCountComponentWithName
                count={count}
                resource={resource}
                resourceType='resources'
                className='resource-image-with-count'/>
            </div>);
        }
      }
    }
  }
  resourceTypes = ['follower'];
  for (var i=0; i<resourceTypes.length; i++){
    resourceType = resourceTypes[i];
    if (organizedResources.hasOwnProperty(resourceType)){
      resources = organizedResources[resourceType];
      components.push(<h5>{resourceType}</h5>);
      for (resource in resources){
        if (resources.hasOwnProperty(resource)){
          count = resources[resource];
          if (count > 0){
            components.push(
              <div>
                <SpanCountComponentWithName
                  count={count}
                  resource={resource}
                  resourceType='followers'
                  className='follower-image-with-count'/>
              </div>);
          }
        }
      }
    }
  }
  return components;
}

function updateResources(data, organizedResources){
  var resourceType;
  var resourceName;
  var playerResources;
  for (resourceName in data['used_resources']){
    if (data['used_resources'].hasOwnProperty(resourceName)){
      for (resourceType in organizedResources){
        if (organizedResources.hasOwnProperty(resourceType)){
          playerResources = organizedResources[resourceType];
          if (playerResources.hasOwnProperty(resourceName)){
            playerResources[resourceName] -= data['used_resources'][resourceName];
          }
        }
      }

    }
  }
  for (resourceName in data['gained_resources']){
    if (data['gained_resources'].hasOwnProperty(resourceName)){
      for (resourceType in organizedResources){
        if (organizedResources.hasOwnProperty(resourceType)){
          playerResources = organizedResources[resourceType];
          if (playerResources.hasOwnProperty(resourceName)){
            playerResources[resourceName] += data['gained_resources'][resourceName];
          }
        }
      }

    }
  }
}
