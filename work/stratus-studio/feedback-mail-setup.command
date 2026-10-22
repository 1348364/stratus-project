#!/bin/zsh
cd -- "${0:A:h}"
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 feedback_mail.py setup
result=$?
if [[ $result -ne 0 ]]; then
  print 'Setup did not finish. Follow the specific message above, then run this file again.'
fi
read '?Press Return to close…'
exit $result
