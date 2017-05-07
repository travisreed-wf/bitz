var BuildingRow = React.createClass({

  componentDidMount() {
    this.timerID = setInterval(
      () => this.props.tickHandler(this.props.buildingIndex),
      1000
    );
  },

  componentWillUnmount() {
    clearInterval(this.timerID);
  },

  _getTotalSpaceInUse: function(){
    return this.props.building.size_per_building * this.props.building.count;
  },

  _getProductionPerTickComponents: function(){
    var components = [];
    var count;
    for (var resource in this.props.building.production_per_tick_dict){
      if (this.props.building.production_per_tick_dict.hasOwnProperty(resource)){
        count = this.props.building.production_per_tick_dict[resource];
      }
      components.push(
        <ResourceImageWithCount
          resource_name={resource}
          count={count}
          separator=' x'/>
      )
    }
    return components;
  },

  _calculateCostAvailable: function() {
    var availableCount = 0;
    var costToUse = this._determineCostToUse();
    var count;
    var playerResources;
    for (var resource in costToUse){
      if (costToUse.hasOwnProperty(resource)){
        count = costToUse[resource];
        for (var resourceType in this.props.organizedResources){
          if (this.props.organizedResources.hasOwnProperty(resourceType)){
            playerResources = this.props.organizedResources[resourceType];
            if (playerResources.hasOwnProperty(resource)){
              var playerCount = playerResources[resource];
              if (playerCount > 0){
                if (playerCount > count){
                  availableCount += count;
                }
                else {
                  availableCount += playerCount;
                }
              }
            }
          }
        }
      }
    }
    return availableCount

  },

  _determineCostToUse: function(){
    if (this.props.building.total_designated_space > this._getTotalSpaceInUse()){
      return this.props.building.discounted_cost;
    }
    else {
      return this.props.building.undiscounted_cost;
    }
  },

  _calculateTotalCost: function() {
    var costToUse = this._determineCostToUse();
    var totalCostCount = 0;

    for (var resource in costToUse) {
      if (costToUse.hasOwnProperty(resource)) {
        var count = costToUse[resource];

        if (count <= 0) {
          continue;
        }

        totalCostCount += count;
      }
    }
    return totalCostCount;
  },

  _getProductionPerDayComponents: function(){
    var components = [];
    var count;
    for (var resource in this.props.building.production_per_tick_dict){
      if (this.props.building.production_per_tick_dict.hasOwnProperty(resource)){
        count = this.props.building.production_per_tick_dict[resource] * this.props.building.ticks_per_day;
      }
      components.push(
        <ResourceImageWithCount
          resource_name={resource}
          count={count}
          separator=' x'/>
      )
    }
    return components;
  },

  _getActionDiv: function(){
    if (this._calculateCostAvailable() >= this._calculateTotalCost()){
      return <button className="btn btn-success" type='button' style={ {width: "100%"} } data-toggle='tooltip' onClick={() => this.props.newBuildingClickHandler(this.props.buildingIndex)}>Build { this.props.building.name }</button>;
    }
    else {
      return (
        <ProgressBarComponent
          leftNumber={ this._calculateCostAvailable()}
          rightNumber={ this._calculateTotalCost()}
          wrapAutomatically={false}/>
      )
    }
  },


  _getCostComponents: function(){
    var components = [];
    var count;
    var cost_to_use;
    var asterisk;
    if (this.props.building.total_designated_space > this._getTotalSpaceInUse()){
      cost_to_use = this.props.building.discounted_cost;
    }
    else {
      asterisk = <span className='extra-cost-asterisk' data-toggle="tooltip" title="Cost increased because no suitable tiles are assigned to this building">*</span>;
      cost_to_use = this.props.building.undiscounted_cost;
    }
    for (var resource in cost_to_use){
      if (cost_to_use.hasOwnProperty(resource)){
        count = cost_to_use[resource]
      }
      components.push(
        <span>
          <ResourceImageWithCount
            resource_name={resource}
            count={count}
            separator=' x'/>
          {asterisk}
        </span>
      )
    }
    return components;
  },
  render: function() {

    return (
      <tr>
        <td style={ {verticalAlign:'middle'} }>
          <img className='building-resource-image' src={"/static/img/resources/" + this.props.building.name + ".png"} /> <span>{this.props.building.name}</span>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getProductionPerTickComponents()}
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <ProgressBarComponent
            leftNumber={this.props.building.seconds_since_last_tick}
            rightNumber={this.props.building.seconds_between_ticks}
            wrapAutomatically={true}/>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getProductionPerDayComponents()}
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getCostComponents() }
        </td>
        <CountComponent
          count={this.props.building.count} />
        <td style={ {verticalAlign:'middle'} }>
          <ProgressBarComponent
          leftNumber={this._getTotalSpaceInUse()}
          rightNumber={this.props.building.total_designated_space}
          extraClassWhenFull='progress-bar-danger'
          wrapAutomatically={false} />
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getActionDiv() }
        </td>
      </tr>
    );
  }

});
