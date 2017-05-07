var FollowerRow = React.createClass({


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
      </tr>
    );
  }

});