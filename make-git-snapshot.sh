#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.
# Point env var REF to a local repo to reduce clone time.

PKG_NAME=mutt-kz
GIT_DIR=$PKG_NAME.git
GIT_URL=git://github.com/karelzak/mutt-kz.git
export GIT_DIR

echo GIT_URL=$GIT_URL
echo GIT_DIR=$GIT_DIR
echo REF=${REF:+--reference $REF}
echo HEAD=${1:-HEAD}

if [[ -d $GIT_DIR ]]; then
    git fetch
else
    git clone --bare ${REF:+--reference $REF} $GIT_URL $GIT_DIR
fi


GIT_SHA=$(git show -s --format='%h')
DIR_NAME=$PKG_NAME-$(date +%Y.%m.%d).git$GIT_SHA
echo DIR_NAME=$DIR_NAME

git archive --format=tar --prefix=$DIR_NAME/ ${1:-HEAD} \
    | xz > $DIR_NAME.tar.xz
