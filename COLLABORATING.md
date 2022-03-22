# Collaborate to the project

If you want to collaborate to the project, here are a few rules that you have to follow

## Commit and pull requests

If you are adding a commit, please place it on your own fork unless you are an administrator. The name of the commit must be of this form : "branch: feature: what you have done". Everything must be in lowercased to be accepted.

## Views

### Api

If you want to add a view to the api, please import the api decorator from api.urls and add the version, app and route in the class of your view that must extend BaseView, ItemView or ListView. You must also add at least permission tests and feature test. It would be nice if you could also add text for special cases.

### Default view

To add a simple view, you must extend one of the utils class listed and add the route to the view in the urls file of the application you are working on. Like the api, please add permission tests and cases tests.