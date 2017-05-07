var ProgressBarComponent = React.createClass({

  getWidth: function() {
    if (this.props.rightNumber == 0){
      return 100
    }
    return (100 * this.props.leftNumber / this.props.rightNumber) % 100;
  },

  _getStrWidth: function() {
    return this.getWidth().toString();
  },

  _getExtraClass: function() {
    if (this.props.leftNumber >= this.props.rightNumber){
      return this.props.extraClassWhenFull
    }
    return '';
  },

  render: function() {
    return (
      <div className="progress">
        <div className={"progress-bar " + this._getExtraClass()} role="progressbar" aria-valuenow={this._getStrWidth()}
          aria-valuemin="0" aria-valuemax="100" style={ {width: this._getStrWidth() + "%" } }>
          {this.props.leftNumber % this.props.rightNumber} / {this.props.rightNumber}
        </div>
      </div>
    )
  }

});

var ResourceImageWithCount = React.createClass({


  render: function() {
    return (
      <span>
        <img className="resource-image-with-count" src={"/static/img/resources/" + this.props.resource_name + ".png"} />
        <span>{this.props.separator} {this.props.count}</span>
      </span>
    )
  }

});

var BuildingRow = React.createClass({

  //getInitialState: function() {
  //
  //  return {
  //    seconds_since_last_tick: this.props.building.seconds_since_last_tick,
  //    seconds_between_ticks: this.props.building.seconds_between_ticks,
  //    production_per_tick_dict: this.props.building.production_per_tick_dict,
  //    total_space_in_use: this.props.building.total_space_in_use,
  //    ticks_per_day: this.props.building.ticks_per_day,
  //    discounted_cost: this.props.building.discounted_cost,
  //    undiscounted_cost: this.props.building.undiscounted_cost,
  //    total_designated_space: this.props.building.total_designated_space || 0,
  //    percent_of_cost_available: this.props.building.percent_of_cost_available
  //  }
  //},



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
    if (this.props.building.percent_of_cost_available >= 100){
      return <button className="btn btn-success" type='button' style={ {width: "100%"} } data-toggle='tooltip' onclick='build(this);'>Build { this.props.building.name }</button>;
    }
    else {
      return (
        <ProgressBarComponent
          leftNumber={ this.props.building.percent_of_cost_available}
          rightNumber={100} />
      )
    }
  },


  _getCostComponents: function(){
    var components = [];
    var count;
    var cost_to_use;
    var asterisk;
    if (this.props.building.total_designated_space > this.props.building.total_space_in_use){
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
            rightNumber={this.props.building.seconds_between_ticks}/>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getProductionPerDayComponents()}
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getCostComponents() }
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <span>{this.props.building.count}</span>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <ProgressBarComponent
          leftNumber={this.props.building.total_space_in_use}
          rightNumber={this.props.building.total_designated_space}
          extraClassWhenFull='progress-bar-danger' />
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getActionDiv() }
        </td>
      </tr>
    );
  }

});
var BuildingTable = React.createClass({

  getInitialState: function() {

    var buildings = JSON.parse('{{ serialized_buildings }}');
    return {
      buildings: buildings
    };
  },

  _getBuildingComponents: function() {
    return this.state.buildings.map((building) =>
      <BuildingRow building={building} />
    );
  },

  render: function() {
    return (
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Production per tick</th>
            <th>Progress toward tick</th>
            <th>Production per day</th>
            <th>Cost</th>
            <th>Count</th>
            <th>Used Space</th>
            <th>Build</th>
          </tr>
        </thead>
        <tbody>
         { this._getBuildingComponents()}
        </tbody>
      </table>
    );
  }

});



ReactDOM.render(
  <BuildingTable />,
  document.getElementById('reactContainer')
);

