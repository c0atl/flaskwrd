from flask import Flask
import flask
import os
import re

app = Flask(__name__)

passwd_file = os.getenv('PASSWD_FILE')
group_file = os.getenv('GROUP_FILE')

@app.route('/')
def home():
    return("Flaskwrd server for querying from your passwd and group files.\n")

@app.route('/users')
def users():
    check_passwd_format()
    users = parse_passwd()
    json_users = passwd_to_json(users)
    return(flask.jsonify(json_users))

@app.route('/users/query')
def users_query():
    check_passwd_format()
    args = {}
    name_query = flask.request.args.getlist('name')
    uid_query = flask.request.args.getlist('uid')
    gid_query = flask.request.args.getlist('gid')
    comment_query = flask.request.args.getlist('comment')
    home_query = flask.request.args.getlist('home')
    shell_query = flask.request.args.getlist('shell')
    if name_query:
        args.update({'name': name_query[0]})
    if uid_query:
        args.update({'uid': uid_query[0]})
    if gid_query:
        args.update({'gid': gid_query[0]})
    if comment_query:
        args.update({'comment': comment_query[0]})
    if home_query:
        args.update({'home': home_query[0]})
    if shell_query:
        args.update({'shell': shell_query[0]})
    matches = parse_passwd(**args)
    user_json = passwd_to_json(matches)
    return(flask.jsonify(user_json))

@app.route('/users/<uid>')
def users_uid(uid):
    check_passwd_format()
    users = parse_passwd(uid=uid)
    # if the list of users is empty, uid was not found, return 404
    if not users:
        flask.abort(404, 'No users matching uid: {}'.format(uid))
    users_json = passwd_to_json(users)
    return(flask.jsonify(users_json))

@app.route('/users/<uid>/groups')
def users_uid_groups(uid):
    check_passwd_format()
    users = parse_passwd(uid=uid)
    # if the list of users is empty, uid was not found, return 404
    if not users:
        flask.abort(404, 'No users matching uid: {}'.format(uid))
    users_json = passwd_to_json(users)
    groups = parse_group(member=".*{}.*".format(users_json[0]['name']))
    group_json = group_to_json(groups)
    return(flask.jsonify(group_json))

@app.route('/groups')
def groups():
    check_group_format()
    groups = parse_group()
    groups_json = group_to_json(groups)
    return(flask.jsonify(groups_json))

@app.route('/groups/query')
def groups_query():
    check_group_format()
    args = {}
    name_query = flask.request.args.getlist('name')
    gid_query = flask.request.args.getlist('gid')
    member_query = flask.request.args.getlist('member')
    if name_query:
        args.update({'name': name_query[0]})
    if gid_query:
        args.update({'gid': gid_query[0]})
    if member_query:
        # for the case when a list of members is passed, match the first one
        # and then loop through the rest of them to check (regex sucks)
        args.update({'member': ".*{}.*".format(member_query[0])})
        matches = parse_group(**args)
        # note: group_dict is actually a list of dicts
        group_dict = group_to_json(matches)
        ret_dict = []
        for entry in group_dict:
            is_match = True
            for member in member_query:
                print(entry['members'])
                print(member)
                if member not in entry['members']:
                    is_match = False
            if is_match: 
                ret_dict.append(entry)
        return(flask.jsonify(ret_dict))

    matches = parse_group(**args)
    group_dict = group_to_json(matches)
    return(flask.jsonify(group_dict))

@app.route('/groups/<gid>')
def groups_gid(gid):
    check_group_format()
    groups = parse_group(gid=gid)
    if not groups:
        flask.abort(404, 'No groups matching gid: {}'.format(gid))
    groups_json = group_to_json(groups)
    return(flask.jsonify(groups_json))
    
def parse_passwd(name='.*', uid='.*', gid='.*', comment='.*', home='.*', shell='.*'):
    try:
        matches = re.findall(r'^{0}:.*:{1}:{2}:{3}:{4}:{5}$'.format(name, uid, gid, comment, home, shell), open(passwd_file).read(), flags=re.MULTILINE)
        return(matches)
    except Exception as e:
        flask.abort(500, "Passwd file does not exist. {}".format(str(e)))

def parse_group(name='.*', gid='.*', member='.*'):
    try:
        matches = re.findall(r'^{0}:.*:{1}:{2}$'.format(name, gid, member), open(group_file).read(), flags=re.MULTILINE)
        return(matches)
    except Exception as e:
        flask.abort(500, "Group file does not exist. {}".format(str(e)))

def passwd_to_json(passwd_list):
    out_list = []
    for passwd_str in passwd_list:
        new_entry = {}
        fields = passwd_str.split(':')
        new_entry.update({'name': fields[0]})
        new_entry.update({'password': fields[1]})
        new_entry.update({'uid': fields[2]})
        new_entry.update({'gid': fields[3]})
        new_entry.update({'comment': fields[4]})
        new_entry.update({'home': fields[5]})
        new_entry.update({'shell': fields[6]})
        out_list.append(new_entry)
    return(out_list)

def group_to_json(group_list):
    out_list = []
    for group_str in group_list:
        new_entry = {}
        fields = group_str.split(':')
        new_entry.update({'name': fields[0]})
        new_entry.update({'password': fields[1]})
        new_entry.update({'gid': fields[2]})
        new_entry.update({'members': fields[3].split(",")})
        out_list.append(new_entry)
    return(out_list)


def check_passwd_format():
    users = parse_passwd()
    if not users:
        flask.abort(500, "No properly formatted passwd entries detected. Passwd file may be malformed")

def check_group_format():
    groups = parse_group()
    if not groups:
        flask.abort(500, "No properly formatted group entries detected. Group file may be malformed")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
