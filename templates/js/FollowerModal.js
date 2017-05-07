var FollowerModal = React.createClass({

  _getSelectOptions: function(){
    var action = this.props.selectedAction;
    console.log('action ');
    console.log(action);
    if (action && action['info_needed']) {
      var options = [];
      var infoNeeded = action['info_needed'];
      if (infoNeeded && infoNeeded.hasOwnProperty('options')) {
        var actionOptions = infoNeeded['options'];
      }
      else {
        actionOptions = [];
      }
      for (var i = 0; i < actionOptions.length; i++) {
        var actionOption = actionOptions[i];
        var option = <option value={actionOption}>{actionOption}</option>;
        options.push(option);
      }
    }
    return options
  },

  render: function() {

    return (
      <div className="modal fade" id="followerModal">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <h4 className="modal-title">Perform Follower Action</h4>
            </div>
            <div className="modal-body">
              <select className="form-control" id="">
                {this._getSelectOptions()}
              </select>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
              <button type="button" className="btn btn-primary">Save changes</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
});
