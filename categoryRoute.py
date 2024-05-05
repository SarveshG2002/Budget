from flask import render_template, request, redirect, url_for, session
from flask_app import app, db
from models import Category
from decorators import login_required

@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if not category_name:
            # If category name is empty, display an error message
            # flash('Category name is required', 'error')
            session['error'] = "Category Name Required"
            return redirect(url_for('category'))

        # Create a new category object and add it to the database session
        new_category = Category(name=category_name,user_id=session['user_id'])
        db.session.add(new_category)
        db.session.commit()

        # Display a success message
        # flash('Category added successfully', 'success')
        session['success'] = "Category created successfully"

        # Redirect to the category page to display the updated list of categories
        return redirect(url_for('category'))
    else:
        categories = Category.query.filter_by(user_id=session['user_id']).all()
        # Render the category page
        return render_template('category.html',categories=categories)
    

@app.route('/delete_category/<int:category_id>', methods=['GET'])
@login_required
def delete_category(category_id):
    # Query the category by its ID
    category = Category.query.get(category_id)
    if category:
        # Delete the category from the database
        db.session.delete(category)
        db.session.commit()
        # flash('Category deleted successfully', 'success')
        session['success'] = "Category deleted successfully"
    else:
        # flash('Category not found', 'error')
        session['error'] = "Category not found"
    # Redirect back to the category page
    return redirect(url_for('category'))


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        # flash('Category not found', 'error')
        session['error'] = "Category not found"
        return redirect(url_for('category'))

    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if not category_name:
            session['error'] = "Category Name Required"
            return redirect(url_for('edit_category', category_id=category_id))

        # Update the category name
        category.name = category_name
        db.session.commit()
        session['success'] = "Category Updated Successfully"
        return redirect(url_for('category'))
    else:
        return render_template('category.html', category=category)

