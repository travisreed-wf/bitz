var FollowerRow = React.createClass({

  _getFollowerActionComponents: function(follower, actions, actionHandler){
    var buttons = [];
    for (let i=0; i<actions.length; i++){
      buttons.push(
        <button
          className="btn btn-success"
          type='button'
          style={ {width: "100%"} }
          data-toggle='tooltip'
          onClick={() => actionHandler(i, follower)}
          >{actions[i].name}</button>);

      buttons.push(<br />);
    }
    return buttons;
  },

  render: function() {

    return (
      <tr>
        <td style={ {verticalAlign:'middle'} }>
          <img className='follower-resource-image' src={"/static/img/followers/" + this.props.follower + ".png"} /> <span>{this.props.follower}</span>
        </td>
        <td>
          <span>{this.props.data.description}</span>
        </td>
        <CountComponent
          count={this.props.count} />
        <td>
          {this._getFollowerActionComponents(
            this.props.follower, this.props.data.actions, this.props.actionHandler
          )}
        </td>
      </tr>
    );
  }

});
