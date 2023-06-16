from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
import logging

error = Blueprint('error', __name__)
logger = logging.getLogger('error_logger')

@error.app_errorhandler(TypeError)
def handle_type_error(error):
	flash(f'Nie masz bezpośredniego dostępu do tej strony (TypeError)', category='error')
	logger.error(f'Bład: {error}.')
	return redirect(url_for('views.dashboard'))

@error.app_errorhandler(ValueError)
def handle_value_error(error):
	flash(f'Nie masz bezpośredniego dostępu do tej strony (ValueError)', category='error')
	logger.error(f'Bład: {error}.')
	return redirect(url_for('views.dashboard'))

@error.app_errorhandler(400)
def handle_400_error(error):
	flash('Operacja nie jest dostępna', category='error')
	logger.error(f'Bład: {error}.')
	return redirect(url_for('views.dashboard'))

@error.app_errorhandler(403)
def handle_403_error(error):
	flash('Brak dostępu do tej strony', category='error')
	logger.error(f'Bład: {error}.')
	return redirect(url_for('views.home'))

@error.app_errorhandler(404)
def page_not_found(error):
    flash('Nie ma takiej strony w tym serwise', category='error')
    logger.error(f'Proba przejscia do niedostepnej strony: {error}.')
    return redirect(url_for('views.home'))
