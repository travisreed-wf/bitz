var CountComponent = React.createClass({

  getInitialState: function () {

    return {
      backgroundColor: ''
    };
  },

  _getStyle: function () {
    if (this.state.backgroundColor){
      return {verticalAlign:'middle', backgroundColor:this.state.backgroundColor};
    }
    else {
      return {verticalAlign:'middle'};
    }
  },

  render: function(){
    return (
      <td style={ this._getStyle() }>
        <span>{this.props.count}</span>
      </td>
    )
  },

  componentDidUpdate(prevProps, prevState){
    if (prevProps.count < this.props.count){
      this.setState({
        backgroundColor: '#5cb85c'
      })
    }
    else if (prevProps.count > this.props.count){
      this.setState({
        backgroundColor: '#d9534f'
      })
    }
    else if (this.state.backgroundColor != '') {
      this.state.backgroundColor = '';
    }
  }
});
