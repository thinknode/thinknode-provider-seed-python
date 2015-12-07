# thinknode-provider-seed-python

A starting point for writing Python calculation providers for Thinknode.

# Use

## Prerequisites

- You have created a Thinknode account.
- You have set up a bucket and development realm in your Thinknode account.
- You have created the app under which this calculation provider will be run.

## Step-by-step Instructions

1. Download this repository.
2. Update the `manifest.json` file with the functions for your app.
3. Add the implementations for the functions in `app.py`.
4. Build the image with `docker build -t registry.thinknode.io/your_account_here/your_app_name_here:your_tag_here .`.
5. Push the image with `docker push registry.thinknode.io/your_account_here/your_app_name_here:your_tag_here`
6. Update the app branch using the current commit id. See [the PATCH /apm/apps/:account/:app/branches/:branch](https://developers.thinknode.com/api/v1.0/services/apm/apps).

Once you install this branch (or release a branch as a version and install the version), you can get a context and start using the app. To test the app seed as it comes in this project, use the following sample calculation request.

```
{
  "function": {
    "account": "your_account_here",
    "app": "your_app_name_here",
    "name": "add",
    "args": [{
      "value": 1
    }, {
      "value": 2
    }]
  }
}
```

Obviously, the result should be `3`.

# Contributing

Please consult the [Contributing](CONTRIBUTING.md) guide.