
set /p version=<distro/version.txt

rem tag the branch with the version number
echo Version created: %version%

rem change to project root directory
cd..
echo Creating tag on branch
git tag -a "%version%" -m "Version %version%"
git push origin %version%

rem Here, we need to commit the file src/app.json that has the up to date change log

git add src/app.json
echo Committing updated app.json to repository
git commit -m "Updating app.json change log with the new version (%version%)."
git push origin master

rem change directory back to the deploy folder
cd deploy

@echo on