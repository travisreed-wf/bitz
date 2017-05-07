var SpanCountComponentWithName = React.createClass({

  getInitialState: function () {

    return {
      backgroundColor: ''
    };
  },

  _getStyle: function () {
    if (this.state.backgroundColor){
      return {paddingBottom: "5px", backgroundColor:this.state.backgroundColor};
    }
    else {
      return {paddingBottom: "5px"};
    }
  },

  render: function(){
    return (
      <span style={this._getStyle()}>
        <img src={"/static/img/" + this.props.resourceType + '/' + this.props.resource + ".png"} className='resource-image-with-count' />  { this.props.resource }: <span>{ this.props.count }</span>
      </span>
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
