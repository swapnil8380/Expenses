from collections import defaultdict
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Group, Expense, User, ExpenseSplit, GroupMember
from app.extensions import db

def register_expense_routes(app):

    @app.route('/groups', methods=['POST'])
    @jwt_required()
    def create_group():
        data = request.json
        user_id = get_jwt_identity()  # Get the ID of the currently authenticated user
        group_name = data.get('name')
        usernames = data.get('usernames', [])

        # Validate inputs
        if not group_name or not usernames:
            return jsonify({"error": "Group name and usernames are required"}), 400

        try:
            # Start a transaction
            with db.session.begin_nested():
                # Create the group
                group = Group(name=group_name, created_by=user_id)
                db.session.add(group)
                db.session.flush()  # Get the group ID before committing

                # Fetch all users in one query to avoid multiple database hits
                users = User.query.filter(User.username.in_(usernames)).all()
                user_dict = {user.username: user for user in users}

                # Check for missing users
                missing_users = set(usernames) - set(user_dict.keys())
                if missing_users:
                    return jsonify({"error": f"Users not found: {', '.join(missing_users)}"}), 404

                # Add users to the group
                group_members = [
                    GroupMember(group_id=group.id, user_id=user.id)
                    for user in user_dict.values()
                ]
                db.session.bulk_save_objects(group_members)

                # Add the creator to the group if not already in the list
                if user_id not in [member.user_id for member in group_members]:
                    creator = GroupMember(group_id=group.id, user_id=user_id)
                    db.session.add(creator)

            # Commit the transaction
            db.session.commit()

            return jsonify({"message": "Group created successfully", "group_id": group.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to create group: {str(e)}"}), 500


    @app.route('/expenses', methods=['POST'])
    @jwt_required()
    def add_expense():
        data = request.json
        user_id = get_jwt_identity()
        #group_name = data.get('name')
        group_id = data.get('group_id')
        amount = data.get('amount')
        description = data.get('description', '')
        involved_usernames = data.get('usernames', [])

        # Validate inputs
        if not group_id or not amount or not involved_usernames:
            return jsonify({"error": "Group ID, amount, and usernames are required"}), 400

        # Check if the group exists and the user is part of it
        group = Group.query.get(group_id)
        if not group:
            return jsonify({"error": "Group not found"}), 404

        if not GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first():
            return jsonify({"error": "You are not a member of this group"}), 403

        # Add the expense
        expense = Expense(group_id=group_id, amount=amount, user_id=user_id, description=description)
        db.session.add(expense)
        db.session.commit()

        # Split the expense among the involved users
        involved_users = []
        for username in involved_usernames:
            user = User.query.filter_by(username=username).first()
            if not user:
                return jsonify({"error": f"User '{username}' not found"}), 404

            if not GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first():
                return jsonify({"error": f"User '{username}' is not a member of this group"}), 400

            involved_users.append(user)

        # Calculate the share per user
        share = amount / len(involved_users)

        for user in involved_users:
            split = ExpenseSplit(expense_id=expense.id, user_id=user.id, amount=share)
            db.session.add(split)

        db.session.commit()
        return jsonify({"message": "Expense added and split among users"}), 201


    @app.route('/expenses/summary', methods=['GET'])
    @jwt_required()
    def expense_summary():
        user_id = get_jwt_identity()

        # Total amount spent by the user
        total_spent = db.session.query(db.func.sum(Expense.amount)) \
            .filter(Expense.user_id == user_id).scalar() or 0

        # Calculate owed amounts
        # Amounts owed to the user (positive balances)
        owed_to_me = db.session.query(User.username, db.func.sum(ExpenseSplit.amount)) \
            .join(Expense, Expense.id == ExpenseSplit.expense_id) \
            .join(User, User.id == ExpenseSplit.user_id) \
            .filter(Expense.user_id == user_id) \
            .group_by(User.username).all()

        # Amounts owed by the user (negative balances)
        owed_to_others = db.session.query(User.username, db.func.sum(ExpenseSplit.amount)) \
            .join(Expense, Expense.id == ExpenseSplit.expense_id) \
            .join(User, User.id == Expense.user_id) \
            .filter(ExpenseSplit.user_id == user_id) \
            .group_by(User.username).all()

        # Combine owed_to_me and owed_to_others into net balances
        balances = defaultdict(float)

        # Add owed_to_me (positive balances)
        for username, amount in owed_to_me:
            balances[username] += float(amount)

        # Add owed_to_others (negative balances)
        for username, amount in owed_to_others:
            balances[username] -= float(amount)

        # Separate into owed_to_me and owed_to_others based on net balance
        final_owed_to_me = [{"username": username, "amount": balance} for username, balance in balances.items() if balance > 0]
        final_owed_to_others = [{"username": username, "amount": abs(balance)} for username, balance in balances.items() if balance < 0]

        # Calculate the total amount owed to the user by others
        amount_owed_to_me = sum(item["amount"] for item in final_owed_to_me)

        # Calculate the total amount owed by the user to others
        amount_owed = sum(item["amount"] for item in final_owed_to_others)

        # Calculate net owned amount (spend - amount owed to me)
        total_owned = amount_owed_to_me - amount_owed

        # Final Response
        return jsonify({
            "total_spent": total_spent,  # Total the user has spent
            "amount_owed": amount_owed,  # Amount the user owes to others
            "amount_owed_to_me": amount_owed_to_me,  # Amount owed to the user by others
            "total_owned": total_owned,  # Final owned amount (spend - owed to the user)
            "owed_to_me": final_owed_to_me,  # Owed to the user (who owes the user)
            "owed_to_others": final_owed_to_others  # Owed by the user (who the user owes)
        }), 200

    @app.route('/groups', methods=['GET'])
    @jwt_required()
    def get_groups():
        try:
            user_id = get_jwt_identity()
            if not GroupMember.query.filter_by(user_id=user_id).first():
                return jsonify({"error": "You are not a member of this group"}), 403 
            groups = Group.query.all()
            group_list = [
                {
                    "id": group.id,
                    "name": group.name,
                    "created_by": group.creator.username,
                    "created_at": group.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "members": [
                        {"id": member.user.id, "username": member.user.username}
                        for member in group.members
                    ]
                }
                for group in groups
            ]
            return jsonify({"groups": group_list}), 200
        except Exception as e:
            return jsonify({"msg": "Error fetching groups", "error": str(e)}), 500