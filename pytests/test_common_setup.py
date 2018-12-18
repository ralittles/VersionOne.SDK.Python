
"""
from testtools import TestCase
from testtools.assertions import assert_that
from testtools.content import text_content
from testtools.matchers import Equals, GreaterThan
"""
import math

import pytest

import v1pysdk


class TestV1CommonSetup():
    def test_initial_create_story(self, v1):
        """Creates a very simple story and returns the object"""
        #v1StoryName = self.getUniqueString()
        #v1StoryName = "sample_story"
        v1StoryName = "tests.query_tests.TestV1Query.test_find_query-1"
        ##self.addDetail('name', text_content(v1StoryName))

        #defaultEstimate = math.fabs(self.getUniqueInteger())
        defaultEstimate = 1.0
        ##self.addDetail('detailedestimate', text_content(str(defaultEstimate)))

        reference = "http://test.com"
        #self.addDetail('reference', text_content(reference))

        scope = v1.Scope.select('Name').page(size=1)
        defaultScope = None
        if len(scope) > 0:
            defaultScope = scope.first()
            #self.addDetail('scope', text_content(defaultScope.Name))
        #else:
            #self.addDetail('scope', text_content('None'))

        epic = v1.Epic.select('Name').page(size=1)
        defaultSuper = None
        if len(epic) > 0:
            defaultSuper = epic.first()
            #self.addDetail('super', text_content(defaultSuper.Name))

        # build a filter string that exactly matches what we've set above
        baseFilterStr = "Reference='" + reference + "'&DetailEstimate='" + str(defaultEstimate) + "'&"
        if defaultScope:
            baseFilterStr += "Scope.Name='" + defaultScope.Name + "'&"
        if defaultSuper:
            baseFilterStr += "Super.Name='" + defaultSuper.Name + "'&"
        baseFilterStr += "Name='" + v1StoryName + "'"

        newStory = None
        try:
            newStory = v1.Story.create(
                Name = v1StoryName,
                Scope = defaultScope,
                Super = defaultSuper,
                DetailEstimate = defaultEstimate,
                Reference = reference,
                )
        except Exception as e:
            pytest.fail("Error creating new story: {0}".format(str(e)))

        #Perform a readback using the constructed filter to make sure the item's on the server
        #self.addDetail('readback-filter', text_content(baseFilterStr))

        createdItems = v1.Story.select('Name').filter(baseFilterStr)
        for t in createdItems: # run query, but don't throw an exception if nothing is returned
            pass

        assert(len(createdItems) > 0, "Created item can't be queried")

        return newStory
