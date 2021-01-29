# Evaluation Script for Udacity HCE Student Blueprints

Please use this script to evaluate student blueprints for course 2 and 3 projects and see the Nutanix.DEV blog article [Evaluations the DevOps Way](https://www.nutanix.dev/2020/12/15/evaluations-the-devops-way/).

## Evaluation App Deployment Instructions

- Obtain a copy of this repository from GitHub.

  Users with access to an environment with `git` already installed, this can be done with the following command.

  ```
  git clone https://github.com/nutanixdev/udacity.git
  ```

  Users that prefer to download this repository using a web browser may follow these steps.

  - Browse to [https://github.com/nutanixdev/udacity.git](https://github.com/nutanixdev/udacity.git)
  - Click the `Code` button and select `Download ZIP`, as shown in the screenshot below.

    ![Download repository as ZIP file](images/download_zip.png)

- Login to Prism Central using the provided credentials
- On the left side of the Prism Central UI, open Nutanix Calm by clicking the "bars" icon, selecting `Services` and clicking `Calm`

  ![Nutanix Calm link](images/services_calm.png)

- When Nutanix Calm opens, select the **Blueprints** button on the left side of the Prism Central UI

  ![Nutanix Calm Blueprints button](images/blueprints.png)

- Click **Upload Blueprint**

  ![Upload Blueprint button](images/upload_blueprint_button.png)

- Browse to the location of this repository on your local workstation and select `HybridCloudEngineer/eval/blueprints/Udacity-HybridCloudEngineer-Evaluation.json`

  ![Upload Blueprint](images/upload_blueprint.png)

  - Because blueprint names must be unique, it is suggested to use **Udacity-HybridCloudEngineer-Evaluation_<initials>**, with **<initials>** replaced by **your** initials
  - The **Project** field may be different for all environments
  - Enter `nutanix4/u` for the **Passphrase**
  - Click **Upload**

  If the upload process is successful, you will be taken directly to the Nutanix Calm blueprint designer for the upload blueprint

- Click the **Launch** button

  ![Launch Blueprint button](images/launch_button.png)

- Complete all fields that can be modified

  - Enter an Application name
  - **EVAL_DIR**: Leave as default, unless you need to change the evaluation directory within the deployed virtual machine
  - **CENTOS_REPO**: Leave as default, unless your environment requires troubleshooting of CentOS package repositories
  - **DEFAULT_PROJECT**: Set this to the name of your Nutanix Calm project, as used when uploading the blueprint in previous steps
  - **PC_PORT**: Leave as default
  - **PC_IP**: Enter the IP address for your Prism Central instance - note this is the **IP Address** only, not the URL

  For example only:

  ![Profile variables](images/profile_variables.png)

  - Click **Service Configuration** and click **UdacityEval**

    ![Service configuration](images/service_configuration.png)

  - Scroll towards the lower part of the deployment settings and ensure the **NIC 1** field is set to a network available in your environment

    ![Select NIC](images/select_nic.png)

  - Click **Credentials** and click **PC_Credentials**

  - Enter the username and password for **your** Prism Central instance

    ![Configure Credentials](images/configure_credentials.png)

    **Note:** Please edit the **teccadmin** credential if you would like to use your own SSH key pair.

  - Click **Create**

    ![Create application button](images/create_button.png)

  - Wait for the Udacity Eval application to finish deploying.  Nutanix Calm will need to download the CentOS 7 disk image and update Linux packages - this may take some time.  A succesful deployment will be indicated by all steps showing as **Finished** and an application state of **RUNNING**.

    ![Deployment finished](images/deployment_finished.png)

  - Click the **Services** tab and select the single service that has been deployed

    ![Select service](images/select_service.png)

  - On the right side of the Nutanix Calm UI, take note of the service's **IP Address**.  An example is shown below - your service's IP address will be different

    ![Service IP address example](images/get_service_ip.png)

## SSH Key Pair (If Required)

If you did not use your own SSH key in earlier steps, the included credential uses the following SSH private and public keys.

### Private key

```
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
```

### Public Key

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDZe5rhzE8oOfjMGBHh/XC1XAgh4nE79gKHroZP51qCATs/uvVNGODplQin1eGfMQvtKv1B/U+FhwQgA5ablYrjAyCw/eM0Sit+Xzg4WFlIAjwoxKeopNVAzh9JnSiCU9E6tFaQw3sB0MwGkwYzdX33oJv3JvspwQxKNp4WvlRdwIiVMdoZ98ZknnRJ2R1cdlNvYnHWChS2/yPyQNBduiLSUyR2+0ou9y+Kd7IqasRMMzdccPpKXwLfLJ8q5NpvszKC6B0KlzEU/v2hh9iomdZcaRSOeHDQ6bMVv/WlYXLxuiH/pXJbvj5HZYvpgcvOakiSFcIWdWpydbXuElX0Vl5MKDB8hk80GqwGnwFRig3RhE05M5ESAy8ePtMmcslPGOFmgqBpydRUY+qPnNcYeHjc+lWuWtHfX8+ml2taj1iSTgjTlu0h65YiXUPh+5dMuX5PINDpZ2GfkmQBuHn0daom6yqHIeLy2CiCHrVN0aKdgLq1VtzQuFcaND+6jxbgrndicNIUeAVfebYW72qByIFj4NGeaukDDp9ZIikorQvBe7nC1poUgPR+knCSmXdVSKjJxRHfSAukuAAiwGVgtHUuMAdAK3JhDtrd20SaWVFguYqZ2jCn6sTj+6JcnBmzx9qCKdeKqkXTcILzitwUw/75XOGi1OD0Ku+4FJXzeBWYew== no-reply@acme.com
```

## Evaluation VM Credentials

- The username for the deployed VM is **teccadmin**.  This user account supports authentication by SSH key pair *only*.

## Student Blueprint Evaluation Instructions

- Obtain exported Nutanix Calm blueprint(s).  The blueprints must be **exported** from the Nutanix Calm UI and not decompiled using the Calm DSL (the JSON output is different between each method).

  Each blueprint will be a single JSON document, when exported correctly.

- Transfer the student blueprint(s) to the evaluation VM deployed by Calm in previous steps.  Because the Udacity evaluation deploys a VM that uses SSH key pair authentication only, the transfer steps will be different depending on method and/or application used.

  Some suggested methods are:

  - SCP (built-in to Linux and Mac systems).  The example below transfers a file named **blueprint1.json** to the **~/nutanix/udacity_eval** directory on the deployed VM, using an SSH key named **udacity**.

    ```
    scp -i ~/.ssh/udacity.pub ~/blueprint1.json teccadmin@<ip address>:~/nutanix/udacity_eval/blueprint1.json
    ```

  - SFTP using [Cyberduck](https://cyberduck.io/).  Cyberduck is recommended as it can make use of PEM-formatted SSH keys as mentioned above, without the need to convert them to PuTTY format.  Please refer to the [Cyberduck SFTP documentation](https://trac.cyberduck.io/wiki/help/en/howto/sftp) for instructions.
  - Any other method of your choice, provided it can connect using SSH key pair

## Script Usage

**Note:** This section assumes you have not altered the **EVAL_DIR** variable from the default - *~/nutanix/udacity_eval/*

- Open an SSH session to the IP address obtained in earlier steps.  The username for the VM is **teccadmin**.

  ```
  ssh teccadmin@<ip_address>
  ```

- Change to the Nutanix Calm DSL directory and activate the required virtual directory

  ```
  cd ~/nutanix/calm-dsl
  . venv/bin/activate
  ```

- Run a quick test to ensure the evaluation script can be executed and does not return any errors

  ```
  cd ~/nutanix/udacity_eval/
  ./eval.bash
  ```

  ![Evaluation script test run](images/eval_test.png)

  The script will make sure the environment is ready to run the evaluations and will exit with usage instructions.

- Student blueprints can now be evaluated.

  If you would like to evaluate all blueprint JSON files in the **~/nutanix/udacity_eval** directory and make sure they match the requirements for Course 3, run the following command:

  ```
  ./eval.bash -c c3.json -d . -b all
  ```

  If you would like to evaluate a specific blueprint JSON file, the syntax can be altered as follows:

  ```
  ./eval.bash -c c3.json -d . -b blueprint1.json
  ```

  The following screenshot shows an example of the script's output, when used to evaluate all blueprints in the current directory.

  ![Evaluation of all blueprints in current directory](images/screenshot.png)

  As you can see, the entire process for two complete blueprints takes seconds only.  Please note the speed of this process may vary slightly depending on individual environments.

### Script Usage Help (If Required)

```
Usage: eval.bash [ARGS]

Args:
  -h  Show this help and exit.
  -d  Location of user blueprints
  -b  Blueprint name to evaluate
  -c  Evaluation criteria file to use for comparison

Note:
  -b  value can be "all", to batch process all JSON blueprints in the specified directory

Examples:
  eval.bash -c eval.json -d ~/blueprints -b blueprint1
  eval.bash -c eval.json -d . -b all
```
